from flask import render_template, request, redirect, url_for, flash, jsonify
from database import db
from models import Donation


def register_routes(app):
    @app.route('/')
    def index():
        """Home page with dashboard"""
        try:
            stats = db.get_dashboard_stats()

            if 'severity_distribution' not in stats or stats['severity_distribution'] is None:
                stats['severity_distribution'] = []

            recent_disasters = db.get_disaster_reports("monthly")[:5]

            for d in recent_disasters:
                try:
                    d['severity'] = int(d['severity'])
                except (ValueError, TypeError):
                    d['severity'] = 0

            recent_news = db.get_disaster_news()[:3]

            return render_template('index.html',
                                   stats=stats,
                                   recent_disasters=recent_disasters,
                                   recent_news=recent_news)
        except Exception as e:
            flash(f"Error loading dashboard: {str(e)}", "error")
            return render_template('index.html',
                                   stats={'severity_distribution': []},
                                   recent_disasters=[],
                                   recent_news=[])

    @app.route('/reports')
    @app.route('/reports/<period>')
    def reports(period='all'):
        """Reports page with filtering"""
        try:
            if period not in ['all', 'weekly', 'monthly', 'yearly']:
                period = 'all'

            disasters = db.get_disaster_reports(period)
            return render_template('reports.html', disasters=disasters, current_period=period)
        except Exception as e:
            flash(f"Error loading reports: {str(e)}", "error")
            return render_template('reports.html', disasters=[], current_period=period)

    @app.route('/donations', methods=['GET', 'POST'])
    def donations():
        """Donations page"""
        if request.method == 'POST':
            try:
                donation = Donation(
                    donor_name=request.form['donor_name'],
                    donor_email=request.form['donor_email'],
                    amount=float(request.form['amount']),
                    disaster_id=int(request.form['disaster_id']) if request.form['disaster_id'] else None,
                    message=request.form['message']
                )

                if db.add_donation(donation):
                    flash("Thank you for your donation!", "success")
                else:
                    flash("Error processing donation. Please try again.", "error")

                return redirect(url_for('donations'))
            except Exception as e:
                flash(f"Error processing donation: {str(e)}", "error")
                return redirect(url_for('donations'))

        try:
            disasters = db.get_disaster_reports()
            donations_list = db.get_donations()
            total_donations = db.get_total_donations()

            return render_template('donations.html',
                                   disasters=disasters,
                                   donations=donations_list,
                                   total_donations=total_donations)
        except Exception as e:
            flash(f"Error loading donations page: {str(e)}", "error")
            return render_template('donations.html', disasters=[], donations=[], total_donations=0)

    @app.route('/safety')
    @app.route('/safety/<disaster_type>')
    def safety(disaster_type=None):
        """Safety measures and policies page"""
        try:
            policies = db.get_safety_policies(disaster_type)
            disaster_types = ['Hurricane', 'Earthquake', 'Wildfire', 'Flood', 'Tornado']

            return render_template('safety.html',
                                   policies=policies,
                                   disaster_types=disaster_types,
                                   current_type=disaster_type)
        except Exception as e:
            flash(f"Error loading safety information: {str(e)}", "error")
            return render_template('safety.html', policies=[], disaster_types=[], current_type=disaster_type)

    @app.route('/news')
    @app.route('/news/<news_type>')
    def news(news_type=None):
        """News, warnings, and predictions page"""
        try:
            news_items = db.get_disaster_news(news_type)
            news_types = ['warning', 'prediction', 'update']

            return render_template('news.html',
                                   news_items=news_items,
                                   news_types=news_types,
                                   current_type=news_type)
        except Exception as e:
            flash(f"Error loading news: {str(e)}", "error")
            return render_template('news.html', news_items=[], news_types=[], current_type=news_type)

    @app.route('/resources')
    def resources():
        """Resource allocation and management page"""
        try:
            resources = db.get_relief_resources()
            allocations = db.get_resource_allocations()

            return render_template('resources.html',
                                   resources=resources,
                                   allocations=allocations)
        except Exception as e:
            flash(f"Error loading resources: {str(e)}", "error")
            return render_template('resources.html', resources=[], allocations=[])

    @app.route('/api/disaster-stats')
    def disaster_stats():
        """API endpoint for disaster statistics"""
        try:
            stats = db.get_dashboard_stats()
            return jsonify(stats)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500
